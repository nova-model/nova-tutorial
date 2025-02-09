FROM savannah.ornl.gov/ndip/nova/carpentry_base


# Copy project files into the container
COPY . /app
WORKDIR /app/lesson-repo

# Build the lesson website (using sandpaper - adjust build command if needed)
RUN Rscript -e "sandpaper::build_lesson()"

CMD ["python3", "-m", "http.server", "8000", "--directory", "/app/site/docs"]
