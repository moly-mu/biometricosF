import './Header.css';

function Header( {title}){
    return(
    <header className="header-form-container">
        <h1 className="main-title">
            <span className='color-i'>I</span>
            <span className='color-u'>U</span>
            <span className='color-d'>D</span>
            <span className='color-c'>C </span>
            {title}</h1>
    </header>
    )
}
export default Header;