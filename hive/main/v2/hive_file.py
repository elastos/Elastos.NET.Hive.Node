import logging
import os
import shutil

from flask import request, Response

from hive.util.common import create_full_path_dir, gene_temp_file_name
from hive.util.did_file_info import get_save_files_path, filter_path_root, query_download, \
    query_properties, query_hash, query_upload_get_filepath, get_dir_size
from hive.util.error_code import INTERNAL_SERVER_ERROR, UNAUTHORIZED, NOT_FOUND, METHOD_NOT_ALLOWED, SUCCESS, FORBIDDEN, \
    BAD_REQUEST
from hive.util.server_response_v2 import ServerResponseV2
from hive.main.v2.pre_proc import post_json_param_pre_proc, pre_proc, get_pre_proc
from hive.util.constants import VAULT_ACCESS_R, VAULT_ACCESS_WR, VAULT_ACCESS_DEL, CHUNK_SIZE
from hive.util.payment.vault_service_manage import can_access_vault, inc_vault_file_use_storage_byte


class HiveFile:
    def __init__(self, app=None):
        self.app = app
        self.response = ServerResponseV2("HiveFile")

    def init_app(self, app):
        self.app = app
        self.app.config['UPLOAD_FOLDER'] = "./temp_file"
        self.app.config['MAX_CONTENT_PATH'] = 10000000
        self.app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

    def move(self, did, app_id, src_name, dst_name, is_copy):
        src_name = filter_path_root(src_name)
        dst_name = filter_path_root(dst_name)

        path = get_save_files_path(did, app_id)
        src_full_path_name = (path / src_name).resolve()
        dst_full_path_name = (path / dst_name).resolve()

        if not src_full_path_name.exists():
            return self.response.response_err(NOT_FOUND, "src_name not exists")

        if dst_full_path_name.exists() and dst_full_path_name.is_file():
            return self.response.response_err(METHOD_NOT_ALLOWED, "dst_name file exists")

        dst_parent_folder = dst_full_path_name.parent
        if not dst_parent_folder.exists():
            if not create_full_path_dir(dst_parent_folder):
                return self.response.response_err(INTERNAL_SERVER_ERROR, "make dst parent path dir error")
        try:
            if is_copy:
                if src_full_path_name.is_file():
                    shutil.copy2(src_full_path_name.as_posix(), dst_full_path_name.as_posix())
                    file_size = os.path.getsize(dst_full_path_name.as_posix())
                    inc_vault_file_use_storage_byte(did, file_size)
                else:
                    shutil.copytree(src_full_path_name.as_posix(), dst_full_path_name.as_posix())
                    dir_size = 0.0
                    dir_size = get_dir_size(dst_full_path_name.as_posix(), dir_size)
                    inc_vault_file_use_storage_byte(did, dir_size)
            else:
                shutil.move(src_full_path_name.as_posix(), dst_full_path_name.as_posix())
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, "Exception:" + str(e))

        return self.response.response_ok()

    def upload_file(self, did, app_id, file_name):
        file_name = filter_path_root(file_name)

        full_path_name, err = query_upload_get_filepath(did, app_id, file_name)
        if err:
            return self.response.response_err(err["status_code"], err["description"])

        temp_file = gene_temp_file_name()
        try:
            with open(temp_file, "bw") as f:
                chunk_size = CHUNK_SIZE
                while True:
                    chunk = request.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    f.write(chunk)
        except Exception as e:
            return self.response.response_err(INTERNAL_SERVER_ERROR, f"Exception: {str(e)}")

        if full_path_name.exists():
            full_path_name.unlink()
        shutil.move(temp_file.as_posix(), full_path_name.as_posix())

        file_size = os.path.getsize(full_path_name.as_posix())
        inc_vault_file_use_storage_byte(did, file_size)
        ret = {"name": file_name}
        return self.response.response_ok(ret, 201)

    def download_file(self, did, app_id, file_name):
        resp = Response()

        data, status_code = query_download(did, app_id, file_name)
        if status_code != SUCCESS:
            if status_code == NOT_FOUND:
                self.response.response_err(status_code, "Not found file")
            elif status_code == FORBIDDEN:
                self.response.response_err(status_code, "Can not download directory")
            return resp
        return data

    def get_property(self, did, app_id, name):
        data, err = query_properties(did, app_id, name)
        if err:
            return self.response.response_err(err["status_code"], err["description"])

        return self.response.response_ok(data)

    def list_files(self, did, app_id, file_name):
        path = get_save_files_path(did, app_id)
        file_name = filter_path_root(file_name)
        full_path_name = (path / file_name).resolve()

        if not (full_path_name.exists() and full_path_name.is_dir()):
            return self.response.response_err(NOT_FOUND, "folder not exists")

        try:
            files = os.listdir(full_path_name.as_posix())
        except Exception as e:
            return self.response.response_ok({"files": []})

        file_info_list = list()
        for file in files:
            full_file = full_path_name / file
            stat_info = full_file.stat()
            if full_file.is_file():
                file_info = {
                    "is_file": True,
                    "name": file,
                    "size": stat_info.st_size
                }
            else:
                file_info = {
                    "is_file": False,
                    "name": file
                }
            file_info_list.append(file_info)

        return self.response.response_ok(file_info_list)

    def file_hash(self, did, app_id, file_name):
        data, err = query_hash(did, app_id, file_name)
        if err:
            return self.response.response_err(err["status_code"], err["description"])

        return self.response.response_ok(data)

    def delete(self, did, app_id, file_name):
        path = get_save_files_path(did, app_id)
        if file_name:
            file_full_name = (path / file_name).resolve()
        else:
            file_full_name = path.resolve()
        if file_full_name.exists():
            if file_full_name.is_dir():
                dir_size = 0.0
                dir_size = get_dir_size(file_full_name.as_posix(), dir_size)
                shutil.rmtree(file_full_name)
                inc_vault_file_use_storage_byte(did, -dir_size)
            else:
                file_size = os.path.getsize(file_full_name.as_posix())
                file_full_name.unlink()
                inc_vault_file_use_storage_byte(did, -file_size)

        return self.response.response_ok(status_code=204)
