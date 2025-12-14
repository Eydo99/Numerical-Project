import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface RootFindingRequest {
  func: string;
  first?: number;
  second?: number;
  tol: number;
  max_itrs: number;
  sig_figs: number;
  single_step: boolean;
  multiplicity?: number | null;
  gx?: string;
}

export interface RootFindingResponse {
  sol: number;
  itrs: number;
  steps: any[];
  exec_time: number;
  status?: number;
  error?: string;
  problem?: string;
}

@Injectable({
  providedIn: 'root',
})
export class RootFindingService {
  private baseUrl = 'http://127.0.0.1:8080';

  constructor(private http: HttpClient) {}

  solve(method: string, payload: RootFindingRequest): Observable<RootFindingResponse> {
    const endpoint = this.getEndpoint(method);
    return this.http.post<RootFindingResponse>(`${this.baseUrl}${endpoint}`, payload);
  }

  plot(funcs: string[], startX: number, endX: number, startY: number, endY: number): Observable<Blob> {
    const payload = {
      funcs: funcs,
      start: startX,
      end: endX,
      starty: startY,
      endy: endY
    };
    return this.http.post(`${this.baseUrl}/plot`, payload, { responseType: 'blob' });
  }

  private getEndpoint(method: string): string {
    const endpoints: { [key: string]: string } = {
      'bisection': '/bisection',
      'false-position': '/false_position',
      'fixed-point': '/fixed_point',
      'newton-orig': '/classic_newton',
      'newton-mod': '/modified_newton',
      'secant': '/secant'
    };
    return endpoints[method] || '/bisection';
  }
}
