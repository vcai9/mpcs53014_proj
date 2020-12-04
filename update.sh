cd ~/proj
rm proj.zip 
zip -r proj.zip bin src appspec.yml
aws --profile mpcs53014 s3 cp proj.zip s3://vycai-mpcs53014/proj.zip
