## Test Batch Log file

### How generate examples logs

- create files:
    ```
    touch /tmp/dns.log
    touch /tmp/apache.log
    ```
- create env and install requirements:
    ```
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
- log command:
    ```
    rlog-generator -p conf/patterns/
    ```

### Running app
    make run

### Down app
    make down
