FROM python:3.11-slim

# Create a non-root user as required by Hugging Face Spaces
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user ./requirements.txt $HOME/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r $HOME/app/requirements.txt

COPY --chown=user . $HOME/app

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "7860"]
