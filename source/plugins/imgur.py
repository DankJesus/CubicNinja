from imgurpython import ImgurClient
class Imgur:
    def __init__(self, clientID, clientSecret):
        # to-do: error check
        self.client = ImgurClient(clientID, clientSecret)

    def uploadPhoto(self, imagePath):
        tempImage = self.client.upload_from_path(imagePath, config=None, anon=True)
        return tempImage['link']

    def deletePhoto(self, imageID):
        self.client.delete_image(imageID)
