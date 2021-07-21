#!/usr/bin/env python
"""Tests for `b_rabbit` package."""
import pytest
from b_rabbit import BRabbit
import rabbitpy
MSG = 'test'
REQUEST_MSG = 'request_msg'
RESPONSE_MSG = 'response_msg'
@pytest.fixture
def rabbit():
    return BRabbit()
def test_connection():
    with pytest.raises(Exception):
        BRabbit(host=1234, port='')
def test_rabbitmq_connection(rabbit):
    assert rabbit
    assert isinstance(rabbit, BRabbit)
    assert isinstance(rabbit.connection, rabbitpy.Connection)


def test_publisher(rabbit):
    properties = BRabbit.Properties(correlation_id = "test_id")
    publisher = rabbit.EventPublisher(b_rabbit=rabbit,
                                      publisher_name='test',
                                      exchange_type='topic',
                                      external=False)
    published = publisher.publish(routing_key='testing.test', payload=MSG, important=False, properties=properties)
    assert published is True


def test_subscriber(rabbit):
    def callback(msg):
        assert msg.body.decode('UTF-8') == MSG
        assert msg.properties["correlation_id"] == "test_id"

    subscriber = rabbit.EventSubscriber(b_rabbit=rabbit,
                                        routing_key='testing.test',
                                        publisher_name='test',
                                        exchange_type='topic',
                                        external=False,
                                        important_subscription=True,
                                        event_listener=callback)
    subscriber.subscribe_on_thread()
    rabbit.close_connection()
