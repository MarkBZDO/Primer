# Document your edge case here
- To get marks for this section you will need to explain to your tutor:
1) The edge case you identified
2) How you have accounted for this in your implementation

# Edge Case: Missing mark

The primer specification says that `mark` is optional when creating a student,
but it does not specify what value should be stored if it is missing.

I chose to store a missing mark as `-1`.

This keeps every student record consistent because each student always has a
numeric mark. It also allows `/stats` to calculate count, average, min, and max
over all student records without needing to skip missing values.

In an extreme case that no student in the database, I return `0` for count, average, min, and max.