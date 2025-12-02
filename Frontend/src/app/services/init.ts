import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})

export class init{
 
    matrix : string[][] = [] ;

    initializeMatrix(matrixSize : number): string[][] {
    return  Array(matrixSize)
      .fill(null)
      .map(() => Array(matrixSize + 1).fill(''));
    }

  initializeGuess(matrixSize : number): number[] {
    return  Array(matrixSize).fill(0);
  }
}