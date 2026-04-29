# KDoc (Kotlin)

Language-specific documentation rules for Kotlin. Apply these in addition to — and where
they conflict, in place of — the generic patterns in `SKILL.md`.

---

## Structure

- The first paragraph (everything before the first blank line) is the **summary
  description**. Everything after is the **detailed description**. Always separate the two
  with a blank line.

```kotlin
/**
 * Returns the user associated with the given ID.
 *
 * Queries the database using [id] and maps the result to a [User]. Returns `null` if no
 * match is found. Throws [IllegalArgumentException] if [id] is negative.
 */
fun getUserById(id: Int): User?
```

---

## Tags

- **Avoid `@param` and `@return`** for routine cases. Incorporate parameter and return
  descriptions directly into the prose, and use `[ParameterName]` link syntax wherever a
  parameter is mentioned.
- Use `@param` and `@return` only when the description is long or complex enough that it
  genuinely does not fit the flow of the main text.
- Use `@throws` (or `@exception`) to document exceptions that callers are expected to
  handle.

```kotlin
// ✅ Preferred — parameters described inline
/**
 * Sends a password-reset email to [email].
 *
 * Returns `true` if the message was accepted by the mail server, `false` if [email] is
 * not associated with any account. Throws [IllegalArgumentException] if [email] is blank.
 */
fun sendPasswordReset(email: String): Boolean

// ⚠️ Use @param / @return only when the description is long
/**
 * Executes [query] against the replica database.
 *
 * @param query The SQL query to execute. Must be a read-only SELECT statement; DML
 *   statements will be rejected by the replica and throw [UnsupportedOperationException].
 * @return A lazy [Sequence] of result rows. The sequence must be consumed within the
 *   current transaction or a [ClosedResourceException] will be raised.
 */
fun executeReadQuery(query: String): Sequence<Row>
```

---

## Style

- Write in the **third person present tense**: "Returns the user", not "Return the user"
  or "This function returns the user".
- **Do not** begin the summary with the element name or a phrase like "This function…" or
  "This class…".
- Use `[Symbol]` link syntax for all references to types, functions, and parameters so
  that generated documentation and IDE tooling can resolve them.

```kotlin
// ✅
/** Computes the SHA-256 digest of [input] and returns it as a hex string. */

// ❌
/** This function will compute the SHA-256 digest of the input. */
```
