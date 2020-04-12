
import os
import json
import boto3
import botocore
from botocore.exceptions import ClientError

# from bpy_lambda import bpy
# import bpy # tested on bpy version 2.80


import bpy


print("IMPORT OK")
print(bpy.app.version_string)

BUCKET_NAME = 'foot-scanning-api'
TMP_DIR = '/tmp/'


def get_s3_keys(bucket):
    s3 = boto3.client('s3')
    """Get a list of keys in an S3 bucket."""
    keys = []
    resp = s3.list_objects_v2(Bucket=bucket)
    for obj in resp['Contents']:
        keys.append(obj['Key'])
    return keys


def obj_to_stl(local_obj_file, local_stl_file):
    # print('Reading', local_obj_file)
    # mesh = read(local_obj_file, file_format='obj')
    # print('Writing as', local_stl_file)
    # write(local_stl_file, mesh, file_format='stl')

    try:
        print('*'*45)
        print("Converting:", local_obj_file)
        print('...File exists', os.path.exists(local_obj_file))
        print('...File size:', os.path.getsize(local_obj_file))
        import_obj = bpy.ops.import_scene.obj(filepath=local_obj_file)

        context = bpy.context
        scene = context.scene
        viewlayer = context.view_layer

        obs = [o for o in scene.objects if o.type == 'MESH']
        bpy.ops.object.select_all(action='DESELECT')    

        for ob in obs:
            viewlayer.objects.active = ob
            ob.select_set(True)
            stl_path = local_stl_file
            bpy.ops.export_mesh.stl(
                    filepath=str(stl_path),
                    use_selection=True)
            ob.select_set(False)
        print("...OK")
    except Exception as e:
        print('Can not convert', local_obj_file)
        print(e)

def lambda_handler(event, context):
    s3 = boto3.resource('s3')

    try:
        # obj=s3.Bucket(BUCKET_NAME).download_file(KEY, LOCAL_FILE)
        keys = get_s3_keys(BUCKET_NAME)
        keys = keys[:1]
        for key in keys:
            file, ext = os.path.splitext(key)
            local_obj_file = TMP_DIR + key
            obj = s3.Bucket(BUCKET_NAME).download_file(key, local_obj_file)
            
            local_stl_file = TMP_DIR + file + '.stl'
            # with open(local_obj_file) as lof:
            #     print('Downloaded object file size:', os.path.getsize(local_obj_file))
            #     with open(local_stl_file, 'w') as lsf:
            #         lsf.write("We writting in this file")
            
            print("converting %s to %s" % (local_obj_file, local_stl_file))

            obj_to_stl(local_obj_file, local_stl_file)
            
            s3_stl_file = os.path.join('data', file+'_converted_.stl')
            s3.meta.client.upload_file(local_stl_file, BUCKET_NAME, s3_stl_file)
            # clear local file from /tmp directory
            os.remove(local_obj_file)
            os.remove(local_stl_file)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

if __name__ == '__main__':
    lambda_handler(None, None)