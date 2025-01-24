FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Install system dependencies: R, git, wget, curl, libxml2-dev, libxslt-dev, libssl-dev, and renv system dependencies
RUN apt-get update && apt-get install -y r-base git wget curl libxml2-dev libxslt-dev libssl-dev \
    libcurl4-openssl-dev \
    libfontconfig-dev \
    libfreetype-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libicu-dev \
    libgit2-dev \
    libjpeg-turbo8-dev \
    libpng-dev \
    libuv1-dev \
    libxslt1-dev \
    libssl-dev \
    libtiff-dev \
    python3 

# Install pandoc 3.1.11
RUN wget https://github.com/jgm/pandoc/releases/download/3.1.11/pandoc-3.1.11-linux-amd64.tar.gz && \
    tar xzf pandoc-3.1.11-linux-amd64.tar.gz -C /tmp/ && \
    mv /tmp/pandoc-3.1.11/bin/pandoc /usr/local/bin/ && \
    rm -rf pandoc-3.1.11-linux-amd64.tar.gz /tmp/pandoc-3.1.11

# Verify pandoc installation
RUN pandoc --version

# Configure R package repositories (including 'archive' now)
RUN R -e "options(repos = list(RSPM = Sys.getenv('RSPM'), carpentries = 'https://carpentries.r-universe.dev/', archive = 'https://carpentries.github.io/drat/', CRAN = 'https://cran.rstudio.com'))"
ENV RSPM="https://packagemanager.posit.co/cran/__linux__/jammy/latest"
# Install remotes R package
RUN R -e "install.packages('remotes', repos = getOption('repos'))"

# Install vise R package (for lesson dependency management)
RUN R -e "remotes::install_github('carpentries/vise')"

# Install R packages: varnish, sandpaper, pegboard (latest versions)
RUN R -e "remotes::install_github('carpentries/varnish')"
RUN R -e "remotes::install_github('carpentries/sandpaper')"
RUN R -e "remotes::install_github('carpentries/pegboard')"

# Copy project files into the container
COPY . /app
WORKDIR /app/lesson-repo

# Build the lesson website (using sandpaper - adjust build command if needed)
RUN Rscript -e "sandpaper::build_lesson()"

CMD ["python3", "-m", "http.server", "8000", "--directory", "/app/site/docs"]
