import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class SolverService {
  coeffMatrix: number[][] = [];
  vectorB: number[] = [];
  parsedMatrix: number[][] = [];

  splitMatrix(matrix: number[][]): void {
    const numRows = matrix.length;
    const numCols = matrix[0].length;

    //clear old values
    this.coeffMatrix = [];
    this.vectorB = [];
    

    for (let i = 0; i < numRows; i++) {
      const row = matrix[i];

      this.coeffMatrix.push(row.slice(0, numCols - 1)); // all except last col
      this.vectorB.push(row[numCols - 1]); // last column
    }
  }

  parseMatrix(stringMatrix: string[][]): number[][] {
    return stringMatrix.map((row: string[]) => {
      return row.map(Number);
    });
  }
  

  private baseUrl = 'http://127.0.0.1:8080';

  constructor(private http: HttpClient) {}

  getSolution(
    size: number,
    matrix: string[][],
    sigFigures: number,
    maxIterations: number,
    tolerance: number,
    initialGuess:number[],
    scaling : boolean,
    endpoint : string
  ) {
    this.parsedMatrix = this.parseMatrix(matrix);
    this.splitMatrix(this.parsedMatrix);

    const payload = {
      dim: size,
      coeff: this.coeffMatrix,
      answers: this.vectorB,
      sig_figs: sigFigures,
      max_itrs: maxIterations,
      tol: tolerance,
      initial:initialGuess as Array<number>,
      scaling : scaling ,
      single_step:true
    };
    console.log(this.coeffMatrix)
    console.log(this.vectorB)
    return this.http.post<any>(`${this.baseUrl}${endpoint}`, payload);
  }
}
