import { Injectable, Query } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '@environment';

@Injectable({
    providedIn: 'root',
})
export class FirmwareService {
    constructor(private httpClient: HttpClient) {}

    async buildFlash(): Promise<void> {
        await this.httpClient.post(`${environment.serverURL}/firmware/build_flash`, null);
    }

    async flashFile(file: File): Promise<void> {
        const formData: FormData = new FormData();
        formData.append('file', file, file.name);
        await this.httpClient.post(`${environment.serverURL}/firmware/flash`, formData).toPromise();
    }

    async getFile(path: string): Promise<string> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("path", path);
        return await this.httpClient.get<string>(`${environment.serverURL}/firmware/get_file`, {params: queryParams}).toPromise();
    }

    async editFile(path: string, content: string): Promise<void> {
        let queryParams = new HttpParams();
        queryParams = queryParams.append("path", path);
        await this.httpClient.post<void>(`${environment.serverURL}/firmware/edit`, content, {params: queryParams}).toPromise();
    }
}
