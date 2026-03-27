import { describe, it, expect } from 'vitest'
import { cn } from './utils'

describe('cn utility', () => {
    it('combines classes correctly', () => {
        expect(cn('btn', 'btn-primary')).toBe('btn btn-primary')
    })

    it('handles conditional classes', () => {
        expect(cn('btn', true && 'active', false && 'hidden')).toBe('btn active')
    })

    it('merges tailwind classes correctly', () => {
        expect(cn('p-4', 'p-2')).toBe('p-2')
    })
})
