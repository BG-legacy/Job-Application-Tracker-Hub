export const formatDate = (dateString) => {
    if (!dateString) return 'No date provided';
    
    try {
        const date = new Date(dateString);
        if (isNaN(date.getTime())) return 'Invalid date';
        
        // Format: "Dec 15, 2023"
        return date.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });
    } catch (error) {
        return 'Invalid date';
    }
}; 