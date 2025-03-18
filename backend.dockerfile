FROM node:18-slim

WORKDIR /home/perplexica

COPY src /home/perplexica/src
COPY tsconfig.json /home/perplexica/
COPY drizzle.config.ts /home/perplexica/
COPY package.json /home/perplexica/
COPY yarn.lock /home/perplexica/

RUN mkdir /home/perplexica/data
RUN mkdir /home/perplexica/uploads
# 安装 Python
RUN apt-get update && apt-get install -y python3 python3-pip
# RUN yarn config set registry 'https://registry.npmmirror.com'
RUN yarn install --frozen-lockfile --network-timeout 600000
RUN yarn build

CMD ["yarn", "start"]