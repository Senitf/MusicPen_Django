from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time
import uuid
import os
from uuid import uuid4
from django.utils import timezone

def get_file_path(instance, filename):
    filename = instance.title + ".jpeg"
    return os.path.join('tmpIMG/%Y/%m/%d', filename)