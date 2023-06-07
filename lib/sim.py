import requests
import redis

def sim_nginx():
    requests.get('http://localhost:8000/')
    requests.get('http://localhost:8000/nonexisting')
    return


def sim_redis():
    # taken from the python examples: https://redis.io/docs/clients/python/
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.set('foo', 'bar')
    r.get('foo')

    r.hset('user-session:123', mapping={
        'name': 'John',
        "surname": 'Smith',
        "company": 'Redis',
        "age": 29
    })

    r.hgetall('user-session:123')

    return


def sim_postgres():
    return


def sim_httpd():
    return


def sim_mongo():
    return


def sim_mysql():
    return


def simulate(key):
    match key:
        case "nginx":
            sim_nginx()
        case "redis":
            sim_redis()
        case "postgres":
            sim_postgres()
        case "httpd":
            sim_httpd()
        case "mysql":
            sim_mysql()

    return
