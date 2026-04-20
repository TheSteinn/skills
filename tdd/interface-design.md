# Interface Design for Testability

Good interfaces make testing natural:

1. **Accept dependencies, don't create them**

    ```
    GOOD: Accept dependency from the caller
    process_order(order, payment_gateway)

    BAD: Create dependency internally
    process_order(order):
      gateway = create_payment_gateway()
    ```

2. **Return results instead of mutating caller-provided state**

    Design interfaces to return explicit results by default. Only use mutation or side-effect-only commands when that behavior is inherently the contract and cannot be expressed more clearly as a returned result.

    ```
    GOOD: Return a result
    discount = calculate_discount(cart)

    BAD: Mutate caller-provided state
    apply_discount(cart)
      cart.total = cart.total - discount
    ```

3. **Small surface area**
   - Fewer methods = fewer tests needed
   - Fewer params = simpler test setup
