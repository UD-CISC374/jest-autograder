
export default class Course {
    name: string;
    units: number;

    constructor(name: string, units: number) {
        if (units < 0) {
            throw new Error('Units can not be negative');
        }

        this.name = name;
        this.units = units;
        return this;
    }

    toString() {
        return `${this.name} (${this.units} units)`;
    }

}