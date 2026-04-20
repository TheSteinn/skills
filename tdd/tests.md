# Good and Bad Tests

## Good Tests

**Integration-style**: Test through real interfaces, not mocks of internal parts.

```
GOOD: Tests observable behavior

TEST "user can checkout with valid cart"
  cart = create_cart()
  cart.add(product)

  result = checkout(cart, payment_method)

  ASSERT result.status == "confirmed"
END
```

Characteristics:

- Tests behavior users/callers care about
- Uses public API only
- Survives internal refactors
- Describes WHAT, not HOW
- One logical assertion per test

## Bad Tests

**Implementation-detail tests**: Coupled to internal structure.

```
BAD: Tests implementation details

TEST "checkout calls payment processor with cart total"
  payment_processor = mock_internal_collaborator()

  checkout(cart, payment_processor)

  ASSERT payment_processor.process WAS_CALLED_WITH cart.total
END
```

Red flags:

- Mocking internal collaborators
- Testing private methods
- Asserting on call counts/order
- Test breaks when refactoring without behavior change
- Test name describes HOW not WHAT
- Verifying through a lower-level mechanism when a stable public interface is available

```
BAD: Bypasses a higher-level interface to verify behavior

TEST "create user saves to storage"
  create_user(name = "Alice")

  row = query_storage("users", where_name = "Alice")

  ASSERT row EXISTS
END

GOOD: Verifies through the public interface

TEST "create user makes user retrievable"
  user = create_user(name = "Alice")
  retrieved = get_user(user.id)

  ASSERT retrieved.name == "Alice"
END

NOTE: If persistence is itself the public contract of the component under test,
asserting on stored state can be correct. Prefer the highest-level stable interface
that matches the behavior you are trying to verify.
```
