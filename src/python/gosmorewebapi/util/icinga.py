warning_counters = {}
critical_counters = {}

warning = 'warning'
critical = 'critical'


def increment(state, key):
    """
    Increment counter
    """
    counter = critical_counters
    if state == 'warning':
        counter = warning_counters
    increment_counter(counter, key)


def increment_counter(counters, key):
    """
    Increment counter
    """
    counter = 0
    if key in counters:
        counter = counters[key]
    counter += 1
    counters[key] = counter


def report():
    state = 'ok'
    if warning_counters:
        state = 'warning'
    if critical_counters:
        state = 'critical'

    ret = {}
    ret['state'] = state
    if critical_counters:
        ret['criticals'] = critical_counters
    if warning_counters:
        ret['warnings'] = warning_counters
    return ret
