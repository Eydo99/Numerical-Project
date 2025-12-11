import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { SolverService } from '../services/solve-service';
import { Helpers } from '../services/helpers';
import { init } from '../services/init';

import { Simulator } from '../components/simulator/simulator';

import { interval, Subject, BehaviorSubject } from 'rxjs';
import { takeUntil, takeWhile, map } from 'rxjs/operators';

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
  selector: 'app-phase1',
  standalone: true,
  imports: [CommonModule, FormsModule, Simulator],
  templateUrl: './phase1.component.html',
  styleUrl: './phase1.component.css'
})
export class Phase1Component {

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

  methods: Method[] = [
    { id: 'gauss', name: 'Gaussian Elimination' },
    { id: 'gauss-jordan', name: 'Gauss-Jordan' },
    { id: 'lu', name: 'LU Decomposition' },
    { id: 'jacobi', name: 'Jacobi Method' },
    { id: 'gauss-seidel', name: 'Gauss-Seidel' }
  ];

  steps: Step[] = [];
  showSimulator = false;
  currentStepIndex$ = new BehaviorSubject<number>(0);
  isPlaying$ = new BehaviorSubject<boolean>(false);
  playbackSpeed: number = 1000;

  private stopPlayback$ = new Subject<void>();

  constructor(
    private solverService: SolverService,
    private cdr: ChangeDetectorRef,
    private helpers: Helpers,
    private initService: init
  ) {
    this.matrix = this.initService.initializeMatrix(this.matrixSize);
    this.initialGuess = this.initService.initializeGuess(this.matrixSize);
  }

  validateInput(): void {
    const validNumberPattern = /^-?\d*\.?\d+(e[+-]?\d+)?$/i;

    this.hasInvalidInput = false;
    this.invalidInputMessage = '';

    for (let i = 0; i < this.matrix.length; i++) {
      for (let j = 0; j < this.matrix[i].length; j++) {
        const value = this.matrix[i][j].trim();

        if (value === '' || value === '-') continue;

        if (!validNumberPattern.test(value)) {
          this.hasInvalidInput = true;
          this.invalidInputMessage = `Invalid input `;
          return;
        }
      }
    }

    if (this.selectedMethod === 'jacobi' || this.selectedMethod === 'gauss-seidel') {
      for (let i = 0; i < this.initialGuess.length; i++) {
        const value = this.initialGuess[i];
        if (!value) continue;
      }
    }
  }

  handleSizeChange(size: number): void {
    this.matrixSize = size;
    this.matrix = this.initService.initializeMatrix(size);
    this.initialGuess = this.initService.initializeGuess(size);
    this.solution = null;
    this.solutionError = null;
    this.executionTime = 0;
    this.iterations = 0;
  }

  loadExample(): void {
    this.matrix = this.helpers.loadExample(this.matrixSize);
  }

  clearMatrix(): void {
    this.matrix = this.initService.initializeMatrix(this.matrixSize);
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

    if (this.hasInvalidInput) return;

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
          if (!res.result) {
            if (res.flags.singular) {
              this.solutionError = 'MATRIX IS SINGULAR';
            } else if (res.flags.asymmetric) {
              this.solutionError = 'MATRIX IS ASYMMETRIC, THE CHOSEN METHOD MAY NOT BE SUITABLE.';
            } else if (res.flags.positive_indef) {
              this.solutionError = "MATRIX ISN'T POSITIVE DEFINITE, THE CHOSEN METHOD MAY NOT BE SUITABLE.";
            }

            this.problemMessage = '';
          } else {
            this.solution = res.result;
            this.executionTime = res.exec_time * 1000 || 0;
            this.iterations = res.itr_cnt || 0;
            this.steps = res.steps || [];
            this.solutionError = null;

            const isDiagonallyDominant = res.flags?.dd;
            const convergenceStatus = res.flags?.conv[0];

            if (isDiagonallyDominant) {
              this.problemMessage = '(THE MATRIX HAS  DIAGONALLY DOMINANT PERMUTATION, CONVERGENCE IS GUARANTEED.)';
            } else if (convergenceStatus === -1) {
              this.problemMessage =
                '(THE MATRIX IS NOT DIAGONALLY DOMINANT, THE SOLUTION MAY OR MAY NOT CONVERGE.)';
            } else if (convergenceStatus === 0) {
              this.problemMessage =
                '(THE MATRIX IS NOT DIAGONALLY DOMINANT. THE SOLUTION DID NOT CONVERGE WITHIN THE ITERATION LIMIT.)';
            } else if (convergenceStatus === 1) {
              this.problemMessage =
                '(THE MATRIX IS NOT DIAGONALLY DOMINANT, BUT THE SOLUTION CONVERGED.)';
            } else {
              this.problemMessage = '';
            }
          }

          this.isLoading = false;
          this.cdr.detectChanges();
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
