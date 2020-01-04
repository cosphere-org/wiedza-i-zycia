import { TestBed } from '@angular/core/testing';

import { WizDataService } from './wiz-data.service';

describe('WizDataService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: WizDataService = TestBed.get(WizDataService);
    expect(service).toBeTruthy();
  });
});
