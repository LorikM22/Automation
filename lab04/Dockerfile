FROM jenkins/ssh-agent

# install PHP-CLI + extensiile cerute de PHPUnit + Composer
RUN apt-get update && apt-get install -y --no-install-recommends \
        php-cli php-xml php-mbstring php-curl \
        unzip git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sS https://getcomposer.org/installer \
    | php -- --install-dir=/usr/local/bin --filename=composer
