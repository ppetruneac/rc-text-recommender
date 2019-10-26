# Requirements for CentOS fresh start. Can use it to run on bash
sudo yum -y update
# sudo yum -y install yum-utils
sudo yum -y groupinstall developments
sudo yum -y install https://centos7.iuscommunity.org/ius-release.rpm
sudo yum install -y python36u python36u-libs python36u-devel python36u-pip
pip install --upgrade pip
sudo yum -y install python36u-devel
mkdir environments
cd environments
python3.6 -m venv rc
source rc/bin/activate
sudo yum install git -y
cd rc-text-recommender
pip install -r requirements.txt