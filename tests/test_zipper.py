""" helpers module """

from ozcore import core
from pytest_httpserver import HTTPServer

    


def test_unzip(test_folder, tmp_folder, clean_tmp):
    # GIVEN zip file in test_folder
    # WHEN downloaded in tmp folder 
    # THEN should be unzipped and zip file removed
    sample = test_folder / "sample.zip"
    server = HTTPServer(port=0)
    s = server.expect_request("/sample.zip", method="GET")
    s.respond_with_data(sample.read_bytes(), mimetype="application/zip")    

    server.start()
    core.utils.unzip(url=server.url_for("/sample.zip"), dest=tmp_folder, chunk_size=1, remove_zip=True)
    server.stop()
    
    assert tmp_folder.joinpath("sample.txt").exists()
    assert not tmp_folder.joinpath("sample.zip").exists()
    
    # clean the tmp folder
    clean_tmp