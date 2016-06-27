## 0.8.2

##### Fixes

###### ORM

- Fixing a possible `Memory Error: stack overflow` error when accessing relations.
- Fixing builder copying process to avoir issues with `PyMySQL`(thanks to [ihumanable](https://github.com/ihumanable)).

###### Commands

- Fixing the `-n/--no-interaction` option not automatically confirming questions.
- Removing the check character in migration commands output to avoid errors on Windows.

###### Connection

- Updating connectors to raise an exception when backend packages are missing.
- Adding standard name resolution to the `purge` method (thanks to [ihumanable](https://github.com/ihumanable)).

###### DBAL

- Fixing setting foreign key constraint name for MySQL.
- Handling missing `constraint_name` for sqlite (thanks to [ihumanable](https://github.com/ihumanable)).


## 0.8.1

##### Fixes

###### ORM

- Removing call to `Model._boot_columns()` to avoid errors for column types not supported by the dbal.

###### Schema Builder

- Fixing `Blueprint.char()` method (thanks to [ihumanable](https://github.com/ihumanable)).
- Fixing `Fluent` behavior.

###### Commands

- Fixing `orator` command not working on Windows.
- Fixing `migrate:status` command not switching databases.

###### Connection

- Fixing a bug when calling `Connnection.disconnect()` after a reconnection when not using read/write connections.
- Fixing `MySQLConnection.get_server_version()` method to be compatible with `PyMySQL` (thanks to [gdraynz](https://github.com/gdraynz)).

## 0.8

##### Improvements

###### ORM

- [#30](https://github.com/sdispater/orator/issues/30) Support for default values
- [#29](https://github.com/sdispater/orator/issues/29) Supporting only one timetamp column on models
- [#26](https://github.com/sdispater/orator/issues/26) Adding support for extra conditions on relationships
- Adding `@scope` decorator to define query scopes.
- Improving global scopes

###### Schema builder

- Adding support for a `use_current()` on timestamps
- Improving dbal to support SQLite fully.
- Improving fluents

###### Query Builder

- [#28](https://github.com/sdispater/orator/issues/28) Making where_in() method accept Collection instances

###### Commands

- Adding a `make:model` command

###### Connection

- Using unicode by default for mysql and postgres.
- Improves how queries are run in `Connection` class

###### Collections

- Adds `flatten()` method to `Collection` class

##### Fixes

###### ORM

- Fixes `Model.get_foreign_key()` method
- Fixes soft deletes
- Avoid going through \_\_setattr\_\_ method when setting timestamps

###### Schema Builder

- [#33](https://github.com/sdispater/orator/issues/33) [SQLite] Renaming or dropping columns loses NULL constraint
- [#32](https://github.com/sdispater/orator/issues/32) [SQLite] Renaming or dropping columns fails when columns' name is a keyword
- [#31](https://github.com/sdispater/orator/issues/31) [SQLite] Changing columns loses default column values.

###### Query Builder

- Fixes query grammar default columns value

###### Connection

- Fixing `Connection._try_again_if_caused_by_lost_connection()` not being called
- Preventing default connection being set to None
- Fixing json type behavior for Postgres

###### Migrations
- Fixing migration stubs


### 0.7.1

(November 30th, 2015)

##### Improvements

- [#20](https://github.com/sdispater/orator/issues/20) Collections have been improved (New methods added)
- Commands have been improved
- The `to_dict` methods on the `Model`, `Collection` classes and paginators are now deprecated. Use `serialize` instead.

##### Fixes

* [#22](https://github.com/sdispater/orator/issues/22) Model.fill() and other methods now accept a dictionary in addition to keyword arguments.
* MySQL charset config value was not used when connecting. This is now fixed. (Thanks to [@heavenshell](https://github.com/heavenshell))
* [#24](https://github.com/sdispater/orator/issues/24) Dynamic properties called the wrong methods when accessing the related items.


### 0.7

(November 10th, 2015)

##### Improvements

- [#15](https://github.com/sdispater/orator/issues/9) Execute migrations inside a transaction.
- [#13](https://github.com/sdispater/orator/issues/9) Support database seeding and model factories.
- [#9](https://github.com/sdispater/orator/issues/9) Support for SQLite foreign keys.
- Relationships decorators.
- Morph relationships now using a name (default being the table name) rather than a class name.

##### Fixes

- [#14](https://github.com/sdispater/orator/issues/14) Changing columns with SchemaBuilder does not work with some types.
- [#16](https://github.com/sdispater/orator/issues/16) The last page of LengthAwarePaginator is not calculated properly in Python 2.7.
- Avoid an error when psycopg2 is not installed.
- Fix dynamic properties for eagerloaded relationships.


### 0.6.4

(July 7th, 2015)

##### Fixes

- [#11](https://github.com/sdispater/orator/issues/11) Paginator.resolve_current_page() raises and error on Python 2.7.


### 0.6.3

(June 30th, 2015)

##### Improvements

- [#10](https://github.com/sdispater/orator/issues/10) Remove hard dependencies in commands.

##### Fixes

- [#8](https://github.com/sdispater/orator/issues/8) Reconnection on lost connection does not properly work.


### 0.6.2

(June 9nd, 2015)

##### Fixes

- Fixes a bug when results rather than the relation was returned
- Starting a new query from a BelongsToMany relation does not maintain pivot columns.
- Model.set_table() method does not properly handle pivot classes.
- Model.fresh() method raises an error for models retrieved from relations.


### 0.6.1

(June 2nd, 2015)

- Fixes a lot of problems that broke relations behavior in 0.6.
- Adds raw() method to orm builder passthru.

### 0.6

(May 31th, 2015)

- Adds pagination support
- Adds model events support
- Implements Model.load() method
- Adds to_json() method to collections
- Makes to_json() methods consistent.
- Fixes how relations are retrieved from strings
- Fixes classes lookup in morph_to() method
- Fixes mutators not being called when initiating models
- Improves models attributes lookup
- Removes DynamicProperty class. Relations are dynamic themselves.

### 0.5

(May 24th, 2015)

- Adds database migrations
- Adds mutators and accessors
- Fix BelongsToMany.save_many() default joinings value

### 0.4

(April 28th, 2015)

- Adds Schema Builder
- Adds scopes support
- Adds support for related name in relationships declaration

### 0.3.1

(April 19th, 2015)

- Fix MySQLdb compatibiity issues
- Fix wrong default key value for Builder.lists() method

### 0.3

(April 3th, 2015)

- Query logging
- Polymorphic relations
- Adds support for Model.has() method
- Adds support for callbacks in eager load conditions
- Adds support for multi-threaded applications by default


### 0.2

(March 31th, 2015)

- Adds actual ORM with relationships and eager loading
- Adds chunk support for QueryBuilder
- Properly close connections when using reconnect() and disconnect() methods


### 0.1

(March 18th, 2015)

- Initial release
