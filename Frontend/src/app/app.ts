// app.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SolverService } from '../services/solve-service';
import { ChangeDetectorRef } from '@angular/core';
import { interval, Subject, BehaviorSubject } from 'rxjs';
import { takeUntil, takeWhile, map } from 'rxjs/operators';
import { Helpers } from '../services/helpers';
import { init } from '../services/init';
import { Simulator } from './components/simulator/simulator';
interface Method {
  id: string;
  name: string;
}
interface Step {
  type: string;
  answers: number[];
  matrix?: number[][];
  L?: number[][];
  U?: number[][];
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule,Simulator],
  templateUrl: 'app.html',
  styles: [
    `
      :host {
        display: block;
      }

      input[type='text']::-webkit-outer-spin-button,
      input[type='text']::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }
    `,
  ],
})
export class App {
  matrixSize = 3;
  selectedMethod = 'gauss';
  sigFigures = 4;
  maxIterations = 100;
  tolerance = 0.0001;
  luAlgorithm = 'doolittle';
  initialGuess: number[] = Array(this.matrixSize).fill(0);
  matrix: string[][] = [];
  solution: number[] | null = null;
  solutionError: string | null = null;
  executionTime: number = 0;
  iterations: number = 0;
  isLoading = false;
  hasInvalidInput = false;
  invalidInputMessage = '';
  problemMessage = '';
  scaling = false;
  currentEndpoint = '';

  constructor(
    private solverService: SolverService,
    private cdr: ChangeDetectorRef,
    private helpers: Helpers,
    private init : init,
  ) {
    this.matrix = init.initializeMatrix(this.matrixSize);
    this.initialGuess = init.initializeGuess(this.matrixSize);
  }

  methods: Method[] = [
    {
      id: 'gauss',
      name: 'Gaussian Elimination',
    },
    {
      id: 'gauss-jordan',
      name: 'Gauss-Jordan',
    },
    {
      id: 'lu',
      name: 'LU Decomposition',
    },
    {
      id: 'jacobi',
      name: 'Jacobi Method',
    },
    {
      id: 'gauss-seidel',
      name: 'Gauss-Seidel',
    },
  ];

  // Step simulator properties
  steps: Step[] = [];
  showSimulator: boolean = false; // Controls visibility
  currentStepIndex$ = new BehaviorSubject<number>(0);
  isPlaying$ = new BehaviorSubject<boolean>(false);
  playbackSpeed: number = 1000; // ms between steps

  private stopPlayback$ = new Subject<void>();

  validateInput(): void {
    const validNumberPattern = /^-?\d*\.?\d+(e[+-]?\d+)?$/i;

    this.hasInvalidInput = false;
    this.invalidInputMessage = '';

    for (let i = 0; i < this.matrix.length; i++) {
      for (let j = 0; j < this.matrix[i].length; j++) {
        const value = this.matrix[i][j].trim();

        // empty cells
        if (value === '' || value === '-') {
          continue;
        }

        if (!validNumberPattern.test(value)) {
          this.hasInvalidInput = true;
          this.invalidInputMessage = `Invalid input `;

          return;
        }
      }
    }

    //initial_guess
    if (this.selectedMethod === 'jacobi' || this.selectedMethod === 'gauss-seidel') {
      for (let i = 0; i < this.initialGuess.length; i++) {
        const value = this.initialGuess[i];

        if (!value) {
          continue;
        }
      }
    }
  }


  handleSizeChange(size: number): void {
    this.matrixSize = size;
    this.matrix = this.init.initializeMatrix(size);
    this.initialGuess = this.init.initializeGuess(size);
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }

  loadExample(): void {
    this.matrix = this.helpers.loadExample(this.matrixSize);
  }

  clearMatrix(): void {
    this.matrix = this.init.initializeMatrix(this.matrixSize);
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }
  

  trackByIndex(index: number): number {
    return index;
  }

  solveSystem(): void {
    this.validateInput();
    console.log(this.matrix);

    if (this.hasInvalidInput) {
      return;
    }

    //reload
    this.isLoading = true;
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.problemMessage = '';
    this.steps = [];
    this.showSimulator = false;

    this.currentEndpoint = this.helpers.getEndpoint(this.selectedMethod, this.luAlgorithm);

    console.log('initialGuess : ' + this.initialGuess);
    console.log(
      'SELECTED METHOD : ' +
        this.selectedMethod +
        ' ' +
        (this.selectedMethod === 'lu' ? this.luAlgorithm : '')
    );

    this.solverService
      .getSolution(
        this.matrixSize,
        this.matrix,
        this.sigFigures,
        this.maxIterations,
        this.tolerance,
        this.initialGuess,
        this.scaling,
        this.currentEndpoint
      )
      .subscribe({
        next: (res) => {
          console.log("itr_cnt : " , res.itr_cnt);
          if (!res.result) {
            console.log(res.flags.singular);
            if (res.flags.singular) this.solutionError = 'MATRIX IS SINGULAR , NO UNIQUE SOLUTION';
            else if (res.flags.asymmetric)
              this.solutionError = 'MATRIX IS ASYMMETRIC , NO SOLUTION';
            else if (res.flags.positive_indef)
              this.solutionError = "MATRIX ISN'T Positive Definite , NO SOLUTION";
            else this.solutionError = 'NO SOLUTION';
          } else {
            this.solution = res.result;
            this.executionTime = res.exec_time * 1000 || 0;
            this.iterations = res.itr_cnt || 0;
            this.steps = res.steps || [];
          }
          
          if (!res.flags?.dd && res.flags?.conv[0] === 0) {
            this.problemMessage =
              "(THE MATRIX ISN'T DIAGONALLY DOMINANT , THE SOLUTION MAY NOT CONVERGE)";
          } else if (res.flags?.conv[0] === -1)
            this.problemMessage =
              "( THE MATRIX ISN'T DIAGONALLY DOMINANT , THE SOLUTION WILL DIVERGE)";
          else if (!res.flags?.dd) this.problemMessage = '(THE MATRIX IS DIAGONALLY DOMINANT) ';
          //else this.problemMessage = "(THE SOLUTION WILL DIVERGE)";

          this.isLoading = false;
          //console.log("no of steps : " ,res.steps.length)

          this.cdr.detectChanges(); // trigger change
        },
        error: (err) => {
          this.solutionError = 'Error solving system';
          this.isLoading = false;
          this.cdr.detectChanges();
        },
      });
  }

  shouldShowScalingOption(): boolean {
    return (
      this.selectedMethod === 'gauss' ||
      this.selectedMethod === 'gauss-jordan' ||
      (this.selectedMethod === 'lu' && this.luAlgorithm === 'dolittle')
    );
  }

  

  // Step simulator controls
  playSimulation(): void {
    if (this.steps.length === 0) return;

    this.isPlaying$.next(true);
    const startIndex = this.currentStepIndex$.value;

    interval(this.playbackSpeed)
      .pipe(
        takeUntil(this.stopPlayback$),
        map((count) => startIndex + count + 1),
        takeWhile((index) => index < this.steps.length)
      )
      .subscribe({
        next: (index) => {
          this.currentStepIndex$.next(index);
          this.cdr.detectChanges();
        },
        complete: () => {
          this.isPlaying$.next(false);
          this.cdr.detectChanges();
        },
      });
  }

  
}
