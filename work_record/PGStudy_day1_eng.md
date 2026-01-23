PostgreSQL
MVCC (Multi-Version Concurrency Control)
Mechanism: When an UPDATE occurs, existing data is not overwritten; instead, a new version of the row is added.

Visibility: Existing rows are marked with XMIN / XMAX (Transaction ID) information so they remain visible only to users (transactions) from before that specific point in time.

Internal Operation: In PostgreSQL, an UPDATE is internally executed as "Delete existing row + Insert new row".

Dead Tuples & Bloat: If a row is updated 5 times, there is only 1 valid data record, but 4 "Dead Tuples" (marked as deleted) remain.

If these are not cleaned up in time, the table swells like a balloon; this phenomenon is called "Bloat."

The database inevitably slows down because it has to scan through Dead Tuples to find valid data.

Q. Is this phenomenon unique to PostgreSQL? How are dead tuples attached to the table? A. The method of stacking previous versions for MVCC (Append-only storage) is a characteristic unique to PostgreSQL (compared to Oracle/MySQL which use Undo segments).

Pro: It allows for long-running transactions without the size limits of an Undo area.

Con: The trade-off is table bloat and the obligation to run VACUUM to clean it up.

Q. Does it always get slower? For example, if we find the live tuple before the dead tuple, wouldn't performance remain the same? A. You might get lucky and find the Live Tuple first to save some CPU cycles, but the correct answer is that it is still slower from an I/O perspective.

Databases read data in "Page" units (typically 8KB), not row by row.

To read 1 valid data item, the DB must read the entire 8KB block containing garbage data.

Garbage data resides in memory, taking up valid cache space (Buffer Cache pollution).

Optimization Issues: You cannot utilize high-speed scanning features like Index-Only Scans (which rely on the Visibility Map).

DBA Response: Check n_dead_tup by querying the pg_stat_user_tables view.

Q. Check examples of actual queries to monitor this.

Clustered Index
Concept: It acts like an English dictionary.

Structure: The data itself is physically sorted in the order of the index key.

Characteristics:

Data is the index, and the index is the data.

Therefore, only one Clustered Index can exist per table.

In PostgreSQL: You can forcibly rearrange the table's data order to match an index using the CLUSTER command.

CLUSTER orders USING order_date_idx; -> PG copies the entire table and rewrites it in the sorted order.

Q. You mentioned rearranging data in "Index Order." What does that mean, and how does it differ from simple data sorting? A. The meaning of CLUSTER (rearranging by index order): The order of the Index Leaf Nodes matches the order in which Data Pages are physically stored.

Rearrangement means accessing each page via the index to fetch data, and then physically storing them in that sorted sequence.

Non-Clustered Index
In PostgreSQL: Most indexes created with CREATE INDEX are non-clustered by default.

Note: Even the Primary Key (PK) in PostgreSQL is non-clustered (unlike MySQL/InnoDB).

Heap Structure: Data is piled up randomly in empty spaces as it comes in (Insert sequence); this is called a Heap.

Inefficiency: While the index helps find data quickly, the TIDs (Block Number, Offset Number) pointed to by the index entries are scattered.

This causes the disk head to move inefficiently, resulting in Random I/O.

Select Query Execution (Internal Workflow)
Q. What is the microscopic operational process when a SELECT query is executed? It goes beyond the abstract concept of "fetching data." A Backend Process performs the work of "scooping up" data in Page units between memory and disk.

Connection: When a Client sends a SELECT request, the Postmaster Process (Listener) detects it and spawns a Backend Process.

Parsing & Planning: The Backend Process checks SQL syntax and determines the most efficient execution path based on statistical information (Cost-based Optimization).

Shared Buffer Check: According to the execution plan, the process looks for data in the Shared Memory area (Shared Buffer) first, rather than going straight to the disk.

It also checks metadata (permissions, table location, etc.) via Catalog information in the Shared Buffer.

Disk Access: If the data is not in the Shared Buffer, it accesses the data files on the disk via the OS file system and reads the pages into memory.

Limitations of CLUSTER in PostgreSQL
One-time Operation: In PG, CLUSTER IDX is a one-time event.

Data Drift: Subsequent INSERT or UPDATE operations will place data into any available empty space (breaking the sort order).

Locking: The CLUSTER command acquires an Exclusive Lock on the table, making it difficult to execute without service downtime.
