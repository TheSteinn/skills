# When to Mock

Mock at **system boundaries** only:

- External APIs (payment, email, etc.)
- Databases (sometimes - prefer test DB)
- Time/randomness
- File system (sometimes)

Don't mock:

- Your own classes/modules
- Internal collaborators
- Anything you control

## Designing for Mockability

At system boundaries, design interfaces that are easy to mock:

**1. Use dependency injection**

Pass external dependencies in rather than creating them internally:

```
GOOD: Easy to mock
process_payment(order, payment_client)
  return payment_client.charge(order.total)

BAD: Hard to mock
process_payment(order)
  client = create_payment_client()
  return client.charge(order.total)
```

**2. Prefer specific boundary operations over generic multi-purpose entry points**

Create specific operations for each external interaction instead of one generic boundary function with conditional logic:

```
GOOD: Each operation is independently mockable
external_service.get_user(user_id)
external_service.get_orders(user_id)
external_service.create_order(order_data)

BAD: Mocking requires conditional logic inside the test double
external_service.call(operation_name, payload)
```

The specific-operation approach means:
- Each test double returns one specific shape
- No conditional logic in test setup
- Easier to see which external operations a test exercises
- Type safety per operation
