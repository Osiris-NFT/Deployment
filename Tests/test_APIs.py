import requests
from settings import *
import json
from PIL import Image
import logging

logger = logging.getLogger("logger")

logger_handler = logging.FileHandler(
    filename="test_logs.log", mode='w')
logger_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"))
logger.setLevel(level=logging.DEBUG)
logger.addHandler(logger_handler)


publication_id = ""
comment_id = ""
reply_id = ""
file_id = ""


def test_if_service_alive():
    response = requests.get(HOST)
    assert response.status_code == 200


def test_post_publication():
    global publication_id
    response = requests.post(HOST + "/api/publications/post",
                             json={
                                 "publication_name": P_NAME,
                                 "user_name": P_USER,
                                 "description": P_DESCR,
                                 "content_type": P_CONTENT,
                                 "category": P_CAT
                             }
                             )
    logger.debug("Post publication response headers: " + str(response.headers))
    logger.debug("Post publication response body: " + response.text)
    json_resp = json.loads(response.text)
    publication_id = json_resp["publication_id"]
    logger.info("Publication ID: " + publication_id)
    assert response.status_code == 200


def test_post_comment():
    global publication_id, comment_id
    response = requests.post(HOST + f"/api/publications/{publication_id}/comments/post",
                             json={
                                 "content": C_CONTENT,
                                 "user": C_USER,
                             }
                             )
    json_resp = json.loads(response.text)
    logger.debug("Post comment response headers: " + str(response.headers))
    logger.debug("Post comment response body: " + response.text)
    comment_id = json_resp["comment"]["_id"]
    logger.info("Comment ID: " + comment_id)
    assert response.status_code == 200


def test_post_reply():
    global publication_id, comment_id, reply_id
    response = requests.post(HOST + f"/api/publications/{publication_id}/comments/{comment_id}/replies/post",
                             json={
                                 "target_user": C_USER,
                                 "content": R_CONTENT,
                                 "user": R_USER,
                             }
                             )
    json_resp = json.loads(response.text)
    logger.debug("Post reply response headers: " + str(response.headers))
    logger.debug("Post reply response body: " + response.text)
    reply_id = json_resp["comment"]["_id"]
    logger.info("Reply ID: " + reply_id)
    assert response.status_code == 200


def test_upload_image():
    global publication_id, file_id
    path_img= "Tests/res/osi.jpg"
    response = requests.post(
        DEBUG_HOST + f"/upload/{publication_id}", files={'file': ("osi.jpg", Image.open(path_img).tobytes(), "image/jpeg", {'Expires': '0'})})
    logger.debug("Upload image response headers: " + str(response.headers))
    logger.debug("Upload image response body: " + response.text)
    json_resp = json.loads(response.text)
    file_id = json_resp["file_id"]
    logger.info("File ID: " + file_id)
    assert response.status_code == 200


def test_download_image():
    global file_id
    response = requests.get(HOST + f"/api/images/{file_id}")
    logger.debug("Download image response headers: " + str(response.headers))
    assert response.status_code == 200


def test_get_publication_by_id():
    global publication_id
    response = requests.get(HOST + f"/api/publications/{publication_id}")
    logger.debug("Get publication by ID response headers: " +
                 str(response.headers))
    logger.debug("Get publication by ID response body: " +
                 response.text)
    assert response.status_code == 200


def test_get_publication_by_user():
    global publication_id
    response = requests.get(HOST + f"/api/{P_USER}/publications")
    logger.debug("Get publication by user response headers: " +
                 str(response.headers))
    logger.debug("Get publication by user response body: " +
                 response.text)
    assert response.status_code == 200


def test_upvote_publication():
    global publication_id
    response = requests.patch(
        HOST + f"/api/publications/{publication_id}/upvote_by/{P_USER}")
    logger.debug("Upvote publication by user response headers: " +
                 str(response.headers))
    logger.debug("Upvote publication by user response body: " +
                 response.text)
    assert response.status_code == 200


def test_confirm_upvote_publication():
    global publication_id
    response = requests.get(
        HOST + f"/api/is/{publication_id}/liked_by/{P_USER}")
    logger.debug("Confirm upvote publication by user response headers: " +
                 str(response.headers))
    logger.debug("Confirm upvote publication by user response body: " +
                 response.text)
    json_resp = json.loads(response.text)
    assert json_resp["is_liked"] is True
    assert response.status_code == 200


def test_get_liked_publication():
    global publication_id
    response = requests.get(
        HOST + f"/api/liked_publications_of/{P_USER}")
    logger.debug("Get upvoted publication by user response headers: " +
                 str(response.headers))
    logger.debug("Get upvoted publication by user response bodKy: " +
                 response.text)
    assert response.status_code == 200


def test_downvote_publication():
    global publication_id
    response = requests.patch(
        HOST + f"/api/publications/{publication_id}/downvoted_by/{P_USER}")
    logger.debug("Downvote publication by user response headers: " +
                 str(response.headers))
    logger.debug("Downvote publication by user response body: " +
                 response.text)
    assert response.status_code == 200


def test_upvote_comment():
    global publication_id, comment_id
    response = requests.patch(
        HOST + f"/api/publications/{publication_id}/comments/{comment_id}/upvote")
    logger.debug("Upvote comment by user response headers: " +
                 str(response.headers))
    logger.debug("Upvote comment by user response body: " +
                 response.text)
    assert response.status_code == 200


def test_downvote_comment():
    global publication_id, comment_id
    response = requests.patch(
        HOST + f"/api/publications/{publication_id}/comments/{comment_id}/downvote")
    logger.debug("Downvote comment by user response headers: " +
                 str(response.headers))
    logger.debug("Downvote comment by user response body: " +
                 response.text)
    assert response.status_code == 200


def test_get_recent_publication():
    global publication_id
    response = requests.get(HOST + "/api/publications/new",
                            params={"hours_time_delta": 1})
    logger.debug("Get recent publication response headers: " +
                 str(response.headers))
    logger.debug("Get recent publication response body: " +
                 response.text)
    assert response.status_code == 200


def test_get_new_best_publication_by_id():
    global publication_id
    response = requests.get(HOST + "/api/publications/new_best")
    logger.debug("Get new best publication response headers: " +
                 str(response.headers))
    logger.debug("Get new best publication response body: " +
                 response.text)
    assert response.status_code == 200


def test_delete_reply_by_id():
    global publication_id, comment_id, reply_id
    response = requests.delete(
        DEBUG_HOST + f"/delete_reply_by_id/{publication_id}/{comment_id}/{reply_id}")
    logger.debug("Delete reply by ID response headers: " +
                 str(response.headers))
    logger.debug("Delete reply by ID response body: " +
                 response.text)
    assert response.status_code == 204


def test_delete_comment_by_id():
    global publication_id, comment_id
    response = requests.delete(
        DEBUG_HOST + f"/delete_comment_by_id/{publication_id}/{comment_id}")
    logger.debug("Delete comment by ID response headers: " +
                 str(response.headers))
    logger.debug("Delete comment by ID response body: " +
                 response.text)
    assert response.status_code == 204


def test_delete_publication_by_id():
    global publication_id
    response = requests.delete(
        DEBUG_HOST + f"/delete_publication_by_id/{publication_id}")
    logger.debug("Delete publication by ID response headers: " +
                 str(response.headers))
    logger.debug("Delete publication by ID response body: " +
                 response.text)
    assert response.status_code == 204
