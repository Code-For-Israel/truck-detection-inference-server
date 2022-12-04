import os
import shutil
import sys
import boto3
import logging


class Files:
    """
    Class Files.
    Handling logger file, local files and folders and on AWS S3 bucket.
    """

    def __init__(self, file_or_dir='', s3_bucket=None, aws_access_key_id=None, aws_secret_access_key=None):
        """
        :param: file_or_dir: the path and name of the file or the folder.
        :param: s3_bucket: the name of the s3 bucket.
        :param: aws_access_key_id: the name of the aws access key id.
        :param: aws_secret_access_key: the name of the secret access key.
        :return: a Files instance.
        """
        if s3_bucket is not None:
            self.bucket = s3_bucket
            self.s3 = boto3.client('s3',
                                   aws_access_key_id=aws_access_key_id,
                                   aws_secret_access_key=aws_secret_access_key)
        self.file = file_or_dir

    def set_logger(self, level=logging.INFO):
        """
        This function creates a logger, by using the logging package, for printing to a log file and to screen.
        :param: level: The level of logging. logging.INFO is the default level.
        :return: The logger
        """
        logger = logging.getLogger(self.file)
        logger.setLevel(level)

        # Create Formatter
        formatter = logging.Formatter(
            '%(asctime)s-%(levelname)s-FILE:%(filename)s-FUNC:%(funcName)s-LINE:%(lineno)d-%(message)s')

        # create a file handler and add it to logger
        file_handler = logging.FileHandler(self.file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        return logger

    def create_folder(self):
        """
        Creating a local folder.
        :return: True or False if folder was created successfully.
        """
        try:
            os.makedirs(self.file, exist_ok=True)
            print("Directory '%s' created successfully" % self.file)
            return True
        except OSError as error:
            print("Directory '%s' can not be created" % self.file)
            return False

    def delete_folder(self):
        """
        Deleting a local folder.
        """
        try:
            shutil.rmtree(self.file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    def delete_images(self):
        """
        Deleting image files.
        """
        for file in os.listdir(self.file):
            if file.startswith("img"):
                os.remove(self.file + '/' + file)
                print(file, 'was deleted')

    def download_from_s3_to_local(self, subfolder):
        """
        Downloading the last file from the s3 bucket.
        :param: subfolder: the folder inside the s3 bucket.
        """
        contents = self.s3.list_objects(Bucket=self.bucket, Prefix=subfolder)['Contents']
        files = [f['Key'] for f in contents]
        self.file = files[-1]
        self.s3.download_file(Filename=subfolder + '/' + self.file, Bucket=self.bucket, Key=self.file)

    def upload_to_s3_from_local(self, file, key=None):
        """
        Uploading a file from local folder to s3 bucket.
        :param: file: the path and name of the file.
        """
        self.file = file
        self.s3.upload_file(Filename=self.file, Bucket=self.bucket, Key=self.file if key is None else key)
