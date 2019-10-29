echo "Deleting Local Files"
rm -rf $HOME/.raula/data/*
echo "Deleting S3 user data"
aws s3 rm --recursive s3://raula-dev-s3bucket-9qu6t4c2729l/
echo "starting module"
python3 -m raula