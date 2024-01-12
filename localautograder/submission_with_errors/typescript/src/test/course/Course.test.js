import Course from "../../course/Course";

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
            // Intentionally broken in student submission to confirm we do not run the students' version
            expect(course.toString()).toBe('foo CMPSC 156 (4 units)');
        });
    });
});