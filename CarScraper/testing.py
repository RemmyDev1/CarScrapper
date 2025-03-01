def have_common_letters(str1, str2):
  """Checks if two strings have any common letters.

  Args:
    str1: The first string.
    str2: The second string.

  Returns:
    True if the strings share at least one letter, False otherwise.
  """

  for letter in str1:
    if letter in str2:
      return True
  return False

# Example usage
print(have_common_letters("hello", "world")) 
print(have_common_letters("cat", "dog"))
