FROM ubuntu

RUN apt-get update && apt-get install -y curl
RUN apt-get install -y gnupg2
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-sdk -y
RUN apt-get install -y git
RUN apt-get install -y pip
RUN git clone https://github.com/zganatra/zganatra-dev.git --branch zganatra-patch-3
RUN pip install setuptools
RUN pip install pandas
RUN pip install google-api-python-client
RUN pip install oauth2client
RUN pip install /zganatra-dev/ai-platform

WORKDIR /zganatra-dev

ENTRYPOINT ["python3", "ai-platform/src/train.py"]
