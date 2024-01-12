import Course from '../../main/course/Course';

describe('Course class tests', () => {
    describe('constructor tests', () => {
        test('(5 pts) can create a Course object', () => {
            const course = new Course('CMPSC 156', 4);
            expect(course.name).toBe('CMPSC 156');
            expect(course.units).toBe(4);
        });
    });

    describe('to string tests', () => {
        test('(5 pts) CMPSC 156 (4 units)', () => {
            const course = new Course('CMPSC 156', 4);
            expect(course.toString()).toBe('CMPSC 156 (4 units)');
        });
    });

    describe('special tests', () => {
        test('(5 pts) A broken, secret test!!secret', () => {
            expect(5).toBe(6);
        });
        test('(5 pts) A broken, hidden test!!hidden', () => {
            expect(5).toBe(6);
        });
        test('(5 pts) A broken, visible test!!visible', () => {
            expect(5).toBe(6);
        });
    });
});