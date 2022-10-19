import os , requests , json , msal
CLIENT_ID = 'f7b8757a-97b5-4822-b712-886bdfc79959'
TENANT_ID = 'a95d9971-30cb-4bcd-aa81-b5122f68aaf3'
AUTHORITY_URL = 'https://login.microsoftonline.com/{}'.format(TENANT_ID)
RESOURCE_URL = 'https://graph.microsoft.com/'
API_VERSION = 'v1.0'
USERNAME = ''
PASSWORD = ''
SCOPES = ['Sites.ReadWrite.All','Files.ReadWrite.All'] 
share_json = {"type" : "view","scope": "anonymous"}
def upload(file_name):

    cognos_to_onedrive = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY_URL)
    token = cognos_to_onedrive.acquire_token_by_username_password(USERNAME,PASSWORD,SCOPES)
    
    headers = {'Authorization': 'Bearer {}'.format(token['access_token'])}
    onedrive_destination = '{}/{}/me/drive/root:/upload'.format(RESOURCE_URL,API_VERSION)
    file_path = "./upload/" + file_name
    file_size = os.stat(file_path).st_size
    if file_size < 4100000:  #簡單上傳
        file_data = open(file_path, 'rb')
        r = requests.put(onedrive_destination+"/"+file_name+":/content", data=file_data, headers=headers)
    else:
        upload_session = requests.post(onedrive_destination+"/"+file_name+":/createUploadSession", headers=headers).json()
        with open(file_path, 'rb') as f:
            total_file_size = os.path.getsize(file_path)
            chunk_size = 32768000 
            chunk_number = total_file_size//chunk_size
            chunk_leftover = total_file_size - chunk_size * chunk_number
            i = 0
            while True:
                chunk_data = f.read(chunk_size)
                start_index = i*chunk_size
                end_index = start_index + chunk_size
                if not chunk_data:
                    break
                if i == chunk_number:
                    end_index = start_index + chunk_leftover
                headers_cut = {'Content-Length':'{}'.format(chunk_size),'Content-Range':'bytes {}-{}/{}'.format(start_index, end_index-1, total_file_size)}
                chunk_data_upload = requests.put(upload_session['uploadUrl'], data=chunk_data, headers=headers_cut)
                #print(chunk_data_upload)
                #print(chunk_data_upload.json())
                i = i + 1
    
    size_p = file_size
    size_q = ["B","KB","MB"]
    q = 0
    while (size_p >= 1024):
        size_p = size_p / 1024.0
        q+=1
    
        
    r = requests.post(onedrive_destination+"/"+ file_name +":/createLink", headers=headers , json=share_json)
    response =  "檔案名稱：" + str(file_name) + "\n" +  \
                "檔案大小：" + str('{:.2f}'.format(size_p)) + str(size_q[q]) + "\n" + \
                "檔案連結：" + str(json.loads(str(r.text))["link"]["webUrl"])

    return response
