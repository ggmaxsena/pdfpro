import useSWR from 'swr'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import fetcher from '../lib/api'

export const useAuth = ({ middleware, redirectIfAuthenticated } = {}) => {
    const router = useRouter()

    const { data: user, error, mutate } = useSWR('/auth/user', url =>
        fetcher(url).catch(error => {
            if (error.status !== 403) throw error
            router.push('/login')
        }),
    )

    const register = async ({ setErrors, ...props }) => {
        setErrors([])

        fetcher('/auth/register/', {
            method: 'POST',
            body: props,
        })
            .then(() => mutate())
            .catch(async error => {
                if (error.status !== 422 && error.status !== 400) throw error
                const errorInfo = await error.info
                setErrors(Object.values(errorInfo).flat())
            })
    }

    const login = async ({ setErrors, setStatus, ...props }) => {
        setErrors([])
        setStatus(null)

        fetcher('/auth/token/', {
            method: 'POST',
            body: props,
        })
            .then(res => {
                localStorage.setItem('auth_token', res.access)
                mutate()
            })
            .catch(async error => {
                if (error.status !== 400) throw error
                const errorInfo = await error.info
                setErrors(Object.values(errorInfo).flat())
            })
    }

    const logout = async () => {
        if (!error) {
            await fetcher('/auth/logout/', { method: 'POST' }).then(() => mutate())
        }

        window.location.pathname = '/login'
    }

    useEffect(() => {
        if (middleware === 'guest' && redirectIfAuthenticated && user) router.push(redirectIfAuthenticated)
        if (middleware === 'auth' && error) router.push('/login')
    }, [user, error])

    return {
        user,
        register,
        login,
        logout,
    }
}
