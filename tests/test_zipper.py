""" helpers module """

from ozcore import core
from pytest_httpserver import HTTPServer

    


def test_unzip_url(test_folder, tmp_folder, clean_tmp):
    # GIVEN zip file in test_folder
    # WHEN downloaded in tmp folder 
    # THEN should be unzipped and zip file removed
    sample = test_folder / "sample.zip"
    server = HTTPServer(port=0)
    s = server.expect_request("/sample.zip", method="GET")
    s.respond_with_data(sample.read_bytes(), mimetype="application/zip")    

    server.start()
    core.utils.unzip_url(url=server.url_for("/sample.zip"), dest=tmp_folder, chunk_size=1, remove_zip=True)
    server.stop()
    
    assert tmp_folder.joinpath("sample.txt").exists()
    assert not tmp_folder.joinpath("sample.zip").exists()
    
    # clean the tmp folder
    clean_tmp
    

def test_backup(test_folder, tmp_folder, clean_tmp):
    # GIVEN three sample files in test folder having toml, txt and yaml extensions
    toml = test_folder / "sample.toml"
    txt = test_folder / "sample.txt"
    yaml = test_folder / "sample.yaml"
    # GIVEN now is core.utils.now_prefix
    now = core.utils.now_prefix("_").split('_')[0]
    # WHEN backup is called from core.utils.backup
    # THEN files are zipped into backup_now....zip
    clean_tmp
    # since now is changing, we need to check _ partials in the zip name
    file=core.utils.backup(src=[toml, txt, yaml], dest=tmp_folder, suffix=None, verbose=True)
    file = core.folder.check_path(file, is_file=True, get_parent=False)
    assert  set(['Backup', now, 'files']).issubset(file.stem.split('_'))
    
    file=core.utils.backup(src=[toml], dest=tmp_folder, suffix=None, verbose=True)
    file = core.folder.check_path(file, is_file=True, get_parent=False)
    assert  set(['Backup', now, 'sample']).issubset(file.stem.split('_'))
    
    file=core.utils.backup(src=toml, dest=tmp_folder, suffix='db', verbose=True)
    file = core.folder.check_path(file, is_file=True, get_parent=False)
    assert  set(['Backup', now, 'db']).issubset(file.stem.split('_'))
       
    """TODO: read zip file contents"""
    # clean the tmp folder
    clean_tmp