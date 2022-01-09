import whois
import urllib3
import dns.resolver
from colorama import Fore, Back, Style, init
from selenium import webdriver
import os


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
http = urllib3.PoolManager()

def ScreenStarter():
  init(autoreset=True)
  print("############################################################################\n")
  print("+-+-+-+-+-+ +-+-+-+-+-+-+-+-+ +-+-+-+-+")
  print(Fore.RED +" |D|o|m|a|i|n| |F|o|l|l|o|w|e|r| ")
  print("+-+-+-+-+-+ +-+-+-+-+-+-+-+-+ +-+-+-+-+")
  print("\n############################ Author : Ali Haydar TOPRAK ####################")

def removeFolder():

    dir = "ScreenShots"
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))

def isRegistered(domain):
    try:
        get_info = whois.whois(domain)
        Status = "Registred"
    except:
        Status = "Not Registered"

    return Status    

def isMxRecord(domain):
    try:
        Status = ""
        for x in dns.resolver.resolve(domain, 'MX'):
            if Status == "":
                Status = x.to_text()
            else:
                Status = Status + "," +x.to_text()
    except:
        Status = "No Record"
    
    return Status

def DomainHTTP_Status(domain,line):

    url = "http://"+line
    try:
        resp = http.request('GET', url, redirect=True, timeout=2.5)
        httpStatus = resp.status
    except urllib3.exceptions.MaxRetryError:
        httpStatus = 'Error'

    return httpStatus   


def DomainHTTPs_Status(domain,line):

    url = "https://"+line
    try:
        resp = http.request('GET', url, redirect=True, timeout=2.5,)
        httpsStatus = resp.status
    except urllib3.exceptions.MaxRetryError:
        httpsStatus = 'Error'

    return httpsStatus

def ScreenShoter(url):
    driver = "chromedriver.exe"
    browser = webdriver.Chrome(executable_path=driver)
    browser.get(url)
    new_string = ''.join(char for char in url if char.isalnum())
    fileName = "ScreenShots"+"\\"+str(new_string)+".png"
    browser.save_screenshot(fileName)
    browser.close()
    return fileName    

def WriteScreen(domain,gStatus,gMxStatus,gHTTP,gHTTPs,HTTP_ScreenShot,HTTPs_ScreenShot):
    print("\n***************************************************")
    print("Domain : {}\nStatus : {}\nMx Record : {}\nHTTP Status : {}\nHTTPs Status : {}\nHTTP SS : {}\nHTTPs SS : {}".format(domain,gStatus,gMxStatus,gHTTP,gHTTPs,HTTP_ScreenShot,HTTPs_ScreenShot))

if __name__ == '__main__':
    ScreenStarter()
    removeFolder()
    with open("sources.txt") as file:
        while (line := file.readline().rstrip()):
            lin = line.split('.')
            domain = str(lin[-2]) +'.'+str(lin[-1])
            gStatus = isRegistered(domain)
            if gStatus == "Registred":
                gMxStatus = isMxRecord(domain)
                gHTTP = DomainHTTP_Status(domain,line)
                if gHTTP != 'Error':
                    url = "http://"+line
                    HTTP_ScreenShot = ScreenShoter(url)
                gHTTPs = DomainHTTPs_Status(domain,line)
                if gHTTPs != 'Error':
                    url = "https://"+line
                    HTTPs_ScreenShot = ScreenShoter(url)
            else:
                gMxStatus = "No Record"
                gHTTP = "ERROR"
                gHTTPs = "ERROR"
                HTTP_ScreenShot = "ERROR"
                HTTPs_ScreenShot = "ERROR"

            WriteScreen(domain,gStatus,gMxStatus,gHTTP,gHTTPs,HTTP_ScreenShot,HTTPs_ScreenShot)