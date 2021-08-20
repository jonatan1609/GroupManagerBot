FROM python:3.9.6-alpine

USER root

RUN \
addgroup -S bot \
&& adduser -DHS -G bot bot \
&& mkdir -p /config \
  && chown -R bot:bot /config \
  && chmod -R 775 /config \
&& apk add --no-cache \
            tini

WORKDIR /opt/bot
COPY . /opt/bot/

RUN \
pip install -r requirements.txt \
&& mv /opt/bot/.config.toml.example /opt/bot/.config.toml.example \
&& chown -R bot:bot /opt/bot

USER bot
VOLUME [ "/config" ]
ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/opt/bot/entrypoint.sh"]
