import { Injectable, Query } from '@angular/core';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { environment } from '@environment';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
    providedIn: 'root',
})
export class FirmwareService {
    constructor(private httpClient: HttpClient) {}

    buildFlash(): Observable<string> {
        return this.httpClient.post(`${environment.serverURL}/firmware/build_flash`, null, {responseType: 'text'})
            .pipe(
                catchError((errorResponse: HttpErrorResponse) => throwError(errorResponse))
            );
    }

    flashFile(file: File): Observable<string> {
        const formData: FormData = new FormData();
        formData.append('file', file, file.name);
        return this.httpClient.post(`${environment.serverURL}/firmware/flash`, formData, {responseType: 'text'})
            .pipe(
                catchError((errorResponse: HttpErrorResponse) => throwError(errorResponse))
            );
    }

    getFile(path: string): Observable<string> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("path", path);
        return this.httpClient.get(`${environment.serverURL}/firmware/get_file`, {params: queryParams, responseType: "text"})
            .pipe(
                catchError((errorResponse: HttpErrorResponse) => throwError(errorResponse))
            );
    }

    editFile(path: string, content: string): Observable<void> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("path", path);
        return this.httpClient.post(`${environment.serverURL}/firmware/edit`, content, {params: queryParams, responseType: "text"})
            .pipe(
                catchError((errorResponse: HttpErrorResponse) => throwError(errorResponse)),
                map(() => {}),
            );
    }
}
