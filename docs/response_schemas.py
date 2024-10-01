from pydantic import BaseModel


class Message(BaseModel):
    detail: str


product_not_found_responses = {
    404: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {"detail": "Product with id 10 not found"}
            }
        }
    }
}


order_not_found_responses = {
    404: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {"detail": "Order with id 10 not found"}
            }
        }
    }
}


create_product_responses = {
    400: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {"detail": "A product named Сахар already exists."}
            }
        }
    }
}


create_order_responses = {
    400: {
        "model": Message,
        "content": {
            "application/json": {
                "examples": {
                    "quantity validation": {
                        "value": {"detail": (
                            "The quantity of the product in the order "
                            "exceeds its availability in stock. "
                            "Quantity Сахар in order: "
                            "100; "
                            "Quantity Сахар in stock: "
                            "10."
                        )}
                    },
                    "order is empty": {
                        "value": {
                            "detail": (
                                "The order is empty. Add items to the order."
                            )
                        }
                    }
                }
            }
        }
    },
    500: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {
                    "detail": (
                        "An error occurred when creating a record "
                        "in the database."
                    )
                }
            }
        }
    }
}


delete_product_responses = {
    200: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {"message": "product successfully delete"}
            }
        }
    },
    404: {
        "model": Message,
        "content": {
            "application/json": {
                "example": {"detail": "Product with id 10 not found"}
            }
        }
    }
}
