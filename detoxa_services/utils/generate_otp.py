from asyncio.log import logger
import requests

def generateMobileOTP(mobile):
    # otp = randint(100000, 999999)
    #### Endpoint to generate OTP
    # https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/AUTOGEN

    ### SAMPLE REQUEST
    otp = requests.get(f'https://2factor.in/API/V1/44b0a5ce-72e9-11ec-b710-0200cd936042/SMS/{mobile}/AUTOGEN')
    # print(otp.json())
    #### Endpoint to verify OTP

    # https://2factor.in/API/V1/{api_key}/SMS/VERIFY/{session_id}/{otp_input}

    ### SAMPLE REQUEST
    # https://2factor.in/API/V1/44b0a5ce-72e9-11ec-b710-0200cd936042/SMS/VERIFY/1223e909-7cfb-44d4-8080-101a4ca9d0c1/866260

    # print(otp.status_code,otp.json()['Details'])
    return otp.json()

def verifyMobileOTP(session_id,otp):
    # otp = randint(100000, 999999)
    #### Endpoint to generate OTP
    # https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/AUTOGEN

    ### SAMPLE REQUEST
    # otp = requests.get(f'https://2factor.in/API/V1/44b0a5ce-72e9-11ec-b710-0200cd936042/SMS/{mobile}/AUTOGEN')
    # print(otp.json())
    #### Endpoint to verify OTP

    otp = requests.get(f'https://2factor.in/API/V1/44b0a5ce-72e9-11ec-b710-0200cd936042/SMS/VERIFY/{session_id}/{otp}')

    ### SAMPLE REQUEST
    # https://2factor.in/API/V1/44b0a5ce-72e9-11ec-b710-0200cd936042/SMS/VERIFY/1223e909-7cfb-44d4-8080-101a4ca9d0c1/866260

    print(otp.status_code,otp.json()['Details'])
    logger.info(otp.status_code,otp.json()['Details'])
    logger.error(otp.status_code,otp.json()['Details'])
    return otp.status_code