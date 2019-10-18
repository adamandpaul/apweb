# -*- coding:utf-8 -*-


def describe_schema(schema_node):
    """A method to return a description of a colander schema"""
    children = []
    for node in schema_node:
        children.append(describe_schema(node))
    return {
        'type': schema_node.typ.__class__.__name__,
        'name': schema_node.name,
        'title': schema_node.title,
        'description': schema_node.description,
        'default': schema_node.default or None,
        'widget': schema_node.widget,
        'children': children,
    }
