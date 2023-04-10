import boto3

# S3 연결 객체 생성
s3 = boto3.resource('s3')

# 버킷 이름
bucket_name = 'hangle-square'

def s3_info():
    # 버킷 객체 수 조회
    bucket_objects = s3.Bucket(bucket_name).objects.all()
    # folder, file count 초기화
    folder_count = 0
    file_count = 0

    for obj in bucket_objects:
        if obj.key.endswith('/'):
            folder_count += 1
        else:
            file_count += 1

    # 버킷 크기 조회 byte로 리턴되기 때문에 Giga Byte 변경
    bucket_size = sum([obj.size for obj in s3.Bucket(bucket_name).objects.all()])/1073741824

    s3_info = {'bucket_name': f'{bucket_name}', 'folder_count': f'{folder_count}', 'file_count': f'{file_count}', 'bucket_size': f'{bucket_size:.2f}G'}
    # bucket 명, 폴더 수, 파일 수, 버킷 사이즈 => 소수점 둘째 자리에서 반올림해서 딕셔너리 형식으로 리턴
    return s3_info