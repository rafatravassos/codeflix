## GENRE domain
### Attributes:
    * id (UUID)
    * name (String)
    * is_active (boolean)
    * categories -> Set[UUID]

### Methods:
    * change_name(str)
    * add_category(UUID)
    * remove_category(UUID)
    * activate()
    * deactivate()

### Use Cases:
    * List genre
    * Create genre
    * Delete genre
    * Update genre