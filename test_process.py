import pytest
from process import process_grades


@pytest.mark.statement
@pytest.mark.parametrize("students, esperado", [
    (
        [
            {'name': 'Ana', 'grades': [80, 90, 85]},    # passed
            {'name': 'Rosa', 'grades': None},           # sin calificaciones
            {'name': 'Luis', 'grades': [60, 60, 60]},   # recovery
            {'name': 'Marta', 'grades': [40, 45, 50]},  # failed
        ],
        {'passed': ['Ana'], 'failed': ['Marta'], 'overall_average': 63.33},
    ),
])
def test_statement_coverage(students, esperado):
    assert process_grades(students) == esperado

@pytest.mark.branch
@pytest.mark.parametrize("students, esperado", [
    # for sin iteraciones, counter == 0
    ([], {'passed': [], 'failed': [], 'overall_average': 0}),
    # grades None (True), counter == 0
    ([{'name': 'Rosa', 'grades': None}],
     {'passed': [], 'failed': [], 'overall_average': 0}),
    # average > 70 (True)
    ([{'name': 'Ana', 'grades': [80, 90, 85]}],
     {'passed': ['Ana'], 'failed': [], 'overall_average': 85.0}),
    # average > 70 (False), >= 50 (True)
    ([{'name': 'Luis', 'grades': [60, 60, 60]}],
     {'passed': [], 'failed': [], 'overall_average': 60.0}),
    # average > 70 (False), >= 50 (False)
    ([{'name': 'Marta', 'grades': [40, 45, 50]}],
     {'passed': [], 'failed': ['Marta'], 'overall_average': 45.0}),
    # frontera exacta 70 (recovery, no passed)
    ([{'name': 'Luis', 'grades': [70, 70, 70]}],
     {'passed': [], 'failed': [], 'overall_average': 70.0}),
    # frontera exacta 50 (recovery, no failed)
    ([{'name': 'Pedro', 'grades': [50, 50, 50]}],
     {'passed': [], 'failed': [], 'overall_average': 50.0}),
])
def test_branch_coverage(students, esperado):
    assert process_grades(students) == esperado


@pytest.mark.branch
def test_empty_grades_raises():
    with pytest.raises(ZeroDivisionError):
        process_grades([{'name': 'Jorge', 'grades': []}])

@pytest.mark.path
@pytest.mark.parametrize("students, esperado", [
    # C1: lista vacia (no entra al for, counter == 0)
    ([], {'passed': [], 'failed': [], 'overall_average': 0}),
    # C2: for -> grades None -> continue
    ([{'name': 'Rosa', 'grades': None}],
     {'passed': [], 'failed': [], 'overall_average': 0}),
    # C3: for -> promedio -> passed -> counter > 0
    ([{'name': 'Ana', 'grades': [80, 90, 85]}],
     {'passed': ['Ana'], 'failed': [], 'overall_average': 85.0}),
    # C4: for -> promedio -> recovery -> counter > 0
    ([{'name': 'Luis', 'grades': [60, 60, 60]}],
     {'passed': [], 'failed': [], 'overall_average': 60.0}),
    # C5: for -> promedio -> failed -> counter > 0
    ([{'name': 'Marta', 'grades': [40, 45, 50]}],
     {'passed': [], 'failed': ['Marta'], 'overall_average': 45.0}),
    # C6: varias iteraciones combinando todos los caminos del loop
    ([
        {'name': 'Ana', 'grades': [80, 90, 85]},
        {'name': 'Rosa', 'grades': None},
        {'name': 'Luis', 'grades': [60, 60, 60]},
        {'name': 'Marta', 'grades': [40, 45, 50]},
    ], {'passed': ['Ana'], 'failed': ['Marta'], 'overall_average': 63.33}),
])
def test_path_coverage(students, esperado):
    assert process_grades(students) == esperado