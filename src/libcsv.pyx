from libc.stdio cimport printf

cdef extern from "libcsv.h":
    void processCsv(
        const char* param1,
        const char* param2,
        const char* param3,
    )
    void processCsvFile(
        const char* param1,
        const char* param2,
        const char* param3,
    )


cdef extern void processCsv(
    const char* param1,
    const char* param2,
    const char* param3,
):
    if param1 is NULL or param2 is NULL or param3 is NULL:
        raise ValueError("Null pointer received in processCsv")

    printf("param1: %s\n", param1)
    printf("param2: %s\n", param2)
    printf("param3: %s\n", param3)


cdef extern void processCsvFile(
    const char* param1,
    const char* param2,
    const char* param3,
):
    if param1 is NULL or param2 is NULL or param3 is NULL:
        raise ValueError("Null pointer received in processCsvFile")

    printf("param1: %s\n", param1)
    printf("param2: %s\n", param2)
    printf("param3: %s\n", param3)